import { Injectable } from "@angular/core";
import { io } from "socket.io-client";
import { Message } from "../models/message.model";

@Injectable({providedIn: 'root'})
export class SocketService {
    socket = io('http://localhost:5000');
    messages: Message[] = []

    constructor() {
        this.socket.on('connect', () => {
            this.socket.send('connected')
        })

        this.socket.on('message', (message: string) => {
            this.messages.push({
                fromUser: false,
                message,
                sendTime: new Date()
            });
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