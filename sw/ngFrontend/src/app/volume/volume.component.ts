import { Component, OnInit } from '@angular/core';
import {BackendService} from '../backend.service';
import {RestAudioService} from './rest-audio.service';

@Component({
  selector: 'app-volume',
  templateUrl: './volume.component.html',
  styleUrls: ['./volume.component.css']
})
export class VolumeComponent implements OnInit {

  mute: any;
  volume: number;
  constructor(private backend: BackendService,
              private restAudio: RestAudioService) { }

  ngOnInit(): void {
    this.restAudio.getVolume().subscribe(json => {
      this.parseVolume(json);
    });
    this.backend.ioSocket.on('volume', json => this.parseVolume(json));
  }

  private parseVolume(json): void {
    this.mute = json.mute;
    this.volume = json.volume;
  }

  volDown(): void {
    this.restAudio.setVolume(this.volume - 2).subscribe(json => {
      this.parseVolume(json);
    });
  }

  volUp(): void {
    this.restAudio.setVolume(this.volume + 2).subscribe(json => {
      this.parseVolume(json);
    });
  }

  toggleMute(): void {
    this.restAudio.toggleMute().subscribe(json => {
      this.parseVolume(json);
    });
  }

  setVol(event): void {
    this.restAudio.setVolume(event).subscribe(json => {
      this.parseVolume(json);
    });
  }
}
