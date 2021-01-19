import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';

@Component({
  selector: 'app-spotify-current',
  templateUrl: './spotify-current.component.html',
  styleUrls: ['./spotify-current.component.css']
})
export class SpotifyCurrentComponent implements OnInit {

  spotifyReport: any;

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
    this.backend.getSpotifyStatus().subscribe(json => {
      this.parseSpotifyStatus(json);
    });
    this.backend.ioSocket.on('spotifyReport', json => this.parseSpotifyStatus(JSON.parse(json)));
  }

  parseSpotifyStatus(json): void {
      this.spotifyReport = json;
      console.log(json);
  }

  turnOn(event: Event): void {
    this.backend.ioSocket.emit('spotify', ['play', 0]);
  }

  turnOff(event: Event): void {
    this.backend.ioSocket.emit('spotify', ['pause', 0]);
  }

  next(event: Event): void {
    console.log('algo');
    this.backend.ioSocket.emit('spotify', ['next', 0]);
  }

  previous(event: Event): void {
    this.backend.ioSocket.emit('spotify', ['previous', 0]);
  }


}
