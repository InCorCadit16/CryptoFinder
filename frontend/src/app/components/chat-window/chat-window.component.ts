import { Component, ElementRef, OnInit } from '@angular/core';
import { SocketService } from 'src/app/services/socket.service';

@Component({
  selector: 'app-chat-window',
  templateUrl: './chat-window.component.html',
  styleUrls: ['./chat-window.component.css']
})
export class ChatWindowComponent implements OnInit {

  constructor(
    private el: ElementRef,
    public socketService: SocketService
  ) { }

  ngOnInit(): void {
    this.socketService.newMessage$.subscribe(msg => {
      setTimeout(() => this.el.nativeElement.scrollBy({ top: this.el.nativeElement.scrollTopMax }), 1);
    });
  }

}
