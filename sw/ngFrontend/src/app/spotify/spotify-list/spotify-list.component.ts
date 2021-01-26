import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';

@Component({
  selector: 'app-spotify-list',
  templateUrl: './spotify-list.component.html',
  styleUrls: ['./spotify-list.component.css']
})
export class SpotifyListComponent implements OnInit {

  spotifyItems: any;

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
    this.backend.getSpotifyItems().subscribe(json => {
      this.parseSpotifyItems(json);
    });
    this.backend.ioSocket.on('spotifyItems', json => this.parseSpotifyItems(JSON.parse(json)));
  }

  parseSpotifyItems(json): void {
      this.spotifyItems = json;
      console.log(json);
  }

  play(uri: any): void {
    this.backend.spotifyPlay(uri).subscribe(json => {
      console.log(json);
    });
  }

  deleteSpotifyItem(idx: number): void {
    console.log('delete idx: ' + idx);
    this.spotifyItems.splice(idx, 1);
    this.backend.deleteSpotifyItem(idx).subscribe(ans => {
        console.log(ans);
      });
  }
}
