import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";
import { io } from "socket.io-client";
import { Message } from "../models/message.model";

@Injectable({providedIn: 'root'})
export class SocketService {
    socket = io('http://localhost:5000');
    messages: Message[] = []
    private newMessage: BehaviorSubject<Message|null> = new BehaviorSubject<Message|null>(null);
    newMessage$: Observable<Message|null> = this.newMessage.asObservable();

    constructor() {
        this.socket.on('connect', () => {
            this.socket.send('connected')
        })

        this.socket.on('message', (message: string) => {
            const msg = {
                fromUser: false,
                message,
                sendTime: new Date()
            };


            this.messages.push(msg);
            this.newMessage.next(msg);
        })
    }

    sendMessage(text: string) {
        this.socket.send(text)
        this.messages.push({
            fromUser: true,
            message: text,
            sendTime: new Date()
        });
    }
    
}