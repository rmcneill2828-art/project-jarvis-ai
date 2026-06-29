"""Tkinter GUI shell for JARVIS OS First Light."""

import tkinter as tk
from tkinter import ttk

from jarvis.config import APP_CONFIG
from jarvis.core import Jarvis
from jarvis.interfaces.conversation import ConversationService


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
            wrap="word",
            state="disabled",
        )
        self._conversation_display.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self._message_entry = ttk.Entry(conversation_frame)
        self._message_entry.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        self._message_entry.bind("<Return>", lambda _event: self._send_message())

        send_button = ttk.Button(conversation_frame, text="Send", command=self._send_message)
        send_button.grid(row=1, column=1, sticky="e", padx=(8, 0), pady=(8, 0))

        service_frame = ttk.LabelFrame(self._root, text="Service Status")
        service_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=(0, 16), pady=8)
        service_frame.columnconfigure(1, weight=1)
        self._service_frame = service_frame

        self._append_message("JARVIS", "First Light online. Type a message to begin.")

    def _send_message(self) -> None:
        message = self._message_entry.get().strip()
        self._message_entry.delete(0, tk.END)

        if message:
            self._append_message("You", message)

        response = self._conversation.respond(message)
        self._append_message("JARVIS", response)

    def _append_message(self, speaker: str, message: str) -> None:
        self._conversation_display.configure(state="normal")
        self._conversation_display.insert(tk.END, f"{speaker}: {message}\n\n")
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
