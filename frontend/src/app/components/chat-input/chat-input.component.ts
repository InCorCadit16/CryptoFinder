import { Component, HostListener, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { SocketService } from 'src/app/services/socket.service';

@Component({
  selector: 'app-chat-input',
  templateUrl: './chat-input.component.html',
  styleUrls: ['./chat-input.component.css']
})
export class ChatInputComponent implements OnInit {
  input: FormControl = new FormControl();

  constructor(private socketService: SocketService) {
    
  }

  ngOnInit(): void {
    
  }

  sendMessage() {
    this.socketService.sendMessage(this.input.value);
    this.input.setValue('');
  }

  @HostListener('document:keypress', ['$event'])
  onEnterPress(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      if (this.input.value != null && this.input.value !== '') { this.sendMessage(); }
    }
  }

}
