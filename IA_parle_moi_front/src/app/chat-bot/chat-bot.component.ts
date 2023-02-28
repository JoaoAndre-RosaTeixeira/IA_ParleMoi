import {Component} from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-chat-bot',
  templateUrl: './chat-bot.component.html',
  styleUrls: ['./chat-bot.component.scss']
})
export class ChatBotComponent {
  isRecording = false;
  apiUrl = 'http://localhost:5000/api';
  recordingUrl = `${this.apiUrl}/start_record`;
  stopUrl = `${this.apiUrl}/stop_record`;
  stopSpeakUrl = `${this.apiUrl}/stop_record`;
  stoprecord: Boolean = false
  speaking: Boolean = false
  response: any;
  question: any;

  constructor(private http: HttpClient) {
  }

  toggleRecording(): void {
    if (this.isRecording) {
      this.stopRecording();
    } else {
      this.startRecording();
    }
  }

  startRecording(): void {
    if (!this.isRecording) {
      this.http.post(this.recordingUrl, {}).subscribe((response: any) => {
        console.log(this.isRecording)
        this.stoprecord = true
        this.isRecording = !this.isRecording;
        console.log(this.isRecording)
      });
    }
  }

  stopRecording(): void {
    if (this.isRecording) {
      if (this.stoprecord){
        this.stoprecord = false
        this.speaking = true
        this.http.post(this.stopUrl, {}).subscribe((response: any) => {
          console.log(this.isRecording)
          this.isRecording = !this.isRecording;
          this.speaking = false
          this.response = response.response
          console.log(this.isRecording)
        });
      }
    }
  }


}
