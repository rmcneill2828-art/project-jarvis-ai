"""Tkinter GUI shell for JARVIS OS First Light."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from jarvis.config import APP_CONFIG
from jarvis.core import Jarvis
from jarvis.interfaces.conversation import (
    TRANSCRIPT_FORMAT_MARKDOWN,
    TRANSCRIPT_FORMAT_TEXT,
    ConversationService,
)


class JarvisApp:
    """First Light GUI shell."""

    def __init__(self, jarvis: Jarvis, conversation: ConversationService | None = None) -> None:
        self._jarvis = jarvis
        self._conversation = conversation or ConversationService()
        self._root = tk.Tk()
        self._root.title(APP_CONFIG.window_title)
        self._root.minsize(720, 520)
        self._orb_growing = True

        self._build_layout()
        self._refresh_services()
        self._animate_orb()
        self._root.protocol("WM_DELETE_WINDOW", self.close)

    def run(self) -> None:
        """Run the GUI event loop."""

        self._root.mainloop()

    def close(self) -> None:
        """Close the GUI shell."""

        self._root.destroy()

    def _build_layout(self) -> None:
        self._root.columnconfigure(0, weight=3)
        self._root.columnconfigure(1, weight=1)
        self._root.rowconfigure(1, weight=1)

        header = ttk.Label(self._root, text="JARVIS OS", font=("Segoe UI", 24, "bold"))
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=16, pady=(16, 8))

        self._orb = tk.Canvas(self._root, width=120, height=120, highlightthickness=0)
        self._orb.grid(row=1, column=0, sticky="n", padx=16, pady=8)
        self._orb_item = self._orb.create_oval(30, 30, 90, 90, fill="#38bdf8", outline="#0f172a")

        conversation_frame = ttk.Frame(self._root)
        conversation_frame.grid(row=2, column=0, sticky="nsew", padx=16, pady=8)
        conversation_frame.columnconfigure(0, weight=1)
        conversation_frame.rowconfigure(0, weight=1)

        self._conversation_display = tk.Text(
            conversation_frame,
            height=12,
            padx=12,
            pady=10,
            wrap="word",
            state="disabled",
        )
        self._conversation_display.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self._configure_conversation_display()

        self._message_entry = ttk.Entry(conversation_frame)
        self._message_entry.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        self._message_entry.bind("<Return>", lambda _event: self._send_message())

        send_button = ttk.Button(conversation_frame, text="Send", command=self._send_message)
        send_button.grid(row=1, column=1, sticky="e", padx=(8, 0), pady=(8, 0))

        new_button = ttk.Button(
            conversation_frame,
            text="New Conversation",
            command=self._new_conversation,
        )
        new_button.grid(row=1, column=2, sticky="e", padx=(8, 0), pady=(8, 0))

        clear_button = ttk.Button(
            conversation_frame,
            text="Clear Conversation",
            command=self._clear_conversation,
        )
        clear_button.grid(row=1, column=3, sticky="e", padx=(8, 0), pady=(8, 0))

        export_frame = ttk.Frame(conversation_frame)
        export_frame.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(8, 0))

        export_markdown_button = ttk.Button(
            export_frame,
            text="Export Markdown",
            command=lambda: self._export_transcript(TRANSCRIPT_FORMAT_MARKDOWN),
        )
        export_markdown_button.grid(row=0, column=0, sticky="w")

        export_text_button = ttk.Button(
            export_frame,
            text="Export Text",
            command=lambda: self._export_transcript(TRANSCRIPT_FORMAT_TEXT),
        )
        export_text_button.grid(row=0, column=1, sticky="w", padx=(8, 0))

        self._conversation_status = ttk.Label(conversation_frame, text="Ready")
        self._conversation_status.grid(row=3, column=0, columnspan=4, sticky="w", pady=(4, 0))

        self._conversation_metadata = ttk.Label(conversation_frame, text="")
        self._conversation_metadata.grid(row=4, column=0, columnspan=4, sticky="w", pady=(2, 0))

        service_frame = ttk.LabelFrame(self._root, text="Service Status")
        service_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=(0, 16), pady=8)
        service_frame.columnconfigure(1, weight=1)
        self._service_frame = service_frame

        self._append_message("JARVIS", "First Light online. Type a message to begin.")
        self._refresh_conversation_metadata()

    def _send_message(self) -> None:
        message = self._message_entry.get().strip()
        self._message_entry.delete(0, tk.END)

        if message:
            self._append_message("You", message)

        self._conversation_status.configure(text="JARVIS is thinking...")
        self._root.update_idletasks()
        response = self._conversation.exchange(message)
        self._append_message("JARVIS", response.message)
        self._conversation_status.configure(text="Ready")
        self._refresh_conversation_metadata()

    def _append_message(self, speaker: str, message: str) -> None:
        self._conversation_display.configure(state="normal")
        speaker_tag = "user_speaker" if speaker == "You" else "jarvis_speaker"
        message_tag = "user_message" if speaker == "You" else "jarvis_message"
        self._conversation_display.insert(tk.END, f"{speaker}\n", speaker_tag)
        self._conversation_display.insert(tk.END, f"{message}\n\n", message_tag)
        self._conversation_display.configure(state="disabled")
        self._conversation_display.see(tk.END)

    def _refresh_services(self) -> None:
        for index, (name, status) in enumerate(self._jarvis.service_statuses().items()):
            ttk.Label(self._service_frame, text=name).grid(
                row=index,
                column=0,
                sticky="w",
                padx=8,
                pady=4,
            )
            ttk.Label(self._service_frame, text=status.value).grid(
                row=index,
                column=1,
                sticky="e",
                padx=8,
                pady=4,
            )

    def _refresh_conversation_metadata(self) -> None:
        metadata = self._conversation.metadata()
        abbreviated_session_id = metadata.session_id[:8]
        self._conversation_metadata.configure(
            text=(
                f"Provider: {metadata.provider} | "
                f"Exchanges: {metadata.exchange_count} | "
                f"Session: {abbreviated_session_id}"
            )
        )

    def _configure_conversation_display(self) -> None:
        self._conversation_display.tag_configure(
            "user_speaker",
            foreground="#1d4ed8",
            font=("Segoe UI", 10, "bold"),
            spacing1=6,
        )
        self._conversation_display.tag_configure(
            "jarvis_speaker",
            foreground="#047857",
            font=("Segoe UI", 10, "bold"),
            spacing1=6,
        )
        self._conversation_display.tag_configure(
            "user_message",
            lmargin1=16,
            lmargin2=16,
            spacing3=8,
        )
        self._conversation_display.tag_configure(
            "jarvis_message",
            lmargin1=16,
            lmargin2=16,
            spacing3=8,
        )

    def _new_conversation(self) -> None:
        self._conversation.new_conversation()
        self._reset_conversation_display()
        self._append_message("JARVIS", "New conversation started.")
        self._conversation_status.configure(text="New conversation ready")
        self._refresh_conversation_metadata()

    def _clear_conversation(self) -> None:
        self._conversation.clear_conversation()
        self._reset_conversation_display()
        self._append_message("JARVIS", "Conversation cleared.")
        self._conversation_status.configure(text="Conversation cleared")
        self._refresh_conversation_metadata()

    def _reset_conversation_display(self) -> None:
        self._conversation_display.configure(state="normal")
        self._conversation_display.delete("1.0", tk.END)
        self._conversation_display.configure(state="disabled")

    def _export_transcript(self, export_format: str) -> None:
        extension = ".md" if export_format == TRANSCRIPT_FORMAT_MARKDOWN else ".txt"
        file_path = filedialog.asksaveasfilename(
            title="Export conversation transcript",
            defaultextension=extension,
            filetypes=(
                ("Markdown files", "*.md"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ),
        )

        if not file_path:
            self._conversation_status.configure(text="Export cancelled")
            return

        try:
            transcript = self._conversation.export_transcript(export_format)
            with open(file_path, "w", encoding="utf-8") as transcript_file:
                transcript_file.write(transcript)
        except OSError as error:
            self._conversation_status.configure(text="Export failed")
            messagebox.showerror("Export failed", str(error))
            return

        self._conversation_status.configure(text=f"Transcript exported to {file_path}")

    def _animate_orb(self) -> None:
        coords = self._orb.coords(self._orb_item)
        left, top, right, bottom = coords

        if self._orb_growing:
            left -= 1
            top -= 1
            right += 1
            bottom += 1
            if right - left >= 76:
                self._orb_growing = False
        else:
            left += 1
            top += 1
            right -= 1
            bottom -= 1
            if right - left <= 60:
                self._orb_growing = True

        self._orb.coords(self._orb_item, left, top, right, bottom)
        self._root.after(80, self._animate_orb)
