import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';
import {RestSpotifyService} from '../rest-spotify.service';

@Component({
  selector: 'app-spotify-list',
  templateUrl: './spotify-list.component.html',
  styleUrls: ['./spotify-list.component.css']
})
export class SpotifyListComponent implements OnInit {

  spotifyItems: any;

  constructor(private backend: BackendService,
              private restSpotify: RestSpotifyService) { }

  ngOnInit(): void {
    this.restSpotify.getSpotifyItems().subscribe(json => {
      this.parseSpotifyItems(json);
    });
    this.backend.ioSocket.on('spotifyItems', json => this.parseSpotifyItems(JSON.parse(json)));
  }

  parseSpotifyItems(json): void {
      this.spotifyItems = json;
      console.log(json);
  }

  play(uri: any): void {
    this.restSpotify.spotifyPlay(uri).subscribe(json => {
      console.log(json);
    });
  }

  deleteSpotifyItem(idx: number): void {
    console.log('delete idx: ' + idx);
    this.spotifyItems.splice(idx, 1);
    this.restSpotify.deleteSpotifyItem(idx).subscribe(ans => {
        console.log(ans);
      });
  }
}
