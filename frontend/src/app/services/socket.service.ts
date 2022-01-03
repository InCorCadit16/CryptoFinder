import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";
import { Message } from "../models/message.model";

@Injectable({providedIn: 'root'})
export class SocketService {
    websocket = new WebSocket('ws://localhost:8081/');
    messages: Message[] = []
    private newMessage: BehaviorSubject<Message|null> = new BehaviorSubject<Message|null>(null);
    newMessage$: Observable<Message|null> = this.newMessage.asObservable();

    constructor() {
        this.websocket.onopen = (ev) => {
            this.websocket.send('connected');
        };

        this.websocket.onmessage = (message: MessageEvent<any>) => {
            const msg = {
                fromUser: false,
                message: message.data,
                sendTime: new Date()
            };


            this.messages.push(msg);
            this.newMessage.next(msg);
        };
    }

    sendMessage(text: string) {
        this.websocket.send(text);
        
        this.messages.push({
            fromUser: true,
            message: text,
            sendTime: new Date()
        });
    }
    
}