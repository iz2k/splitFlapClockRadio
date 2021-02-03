import { Component, OnInit } from '@angular/core';
import {BackendService} from '../backend.service';

@Component({
  selector: 'app-volume',
  templateUrl: './volume.component.html',
  styleUrls: ['./volume.component.css']
})
export class VolumeComponent implements OnInit {

  mute: any;
  volume: number;
  constructor(private backend: BackendService) { }

  ngOnInit(): void {
    this.backend.getVolume().subscribe(json => {
      this.parseVolume(json);
    });
    this.backend.ioSocket.on('volume', json => this.parseVolume(json));
  }

  private parseVolume(json): void {
    this.mute = json.mute;
    this.volume = json.volume;
  }

  volDown(): void {
    this.backend.setVolume(this.volume - 2).subscribe(json => {
      this.parseVolume(json);
    });
  }

  volUp(): void {
    this.backend.setVolume(this.volume + 2).subscribe(json => {
      this.parseVolume(json);
    });
  }

  toggleMute(): void {
    this.backend.toggleMute().subscribe(json => {
      this.parseVolume(json);
    });
  }

  setVol(event): void {
    this.backend.setVolume(event).subscribe(json => {
      this.parseVolume(json);
    });
  }
}
