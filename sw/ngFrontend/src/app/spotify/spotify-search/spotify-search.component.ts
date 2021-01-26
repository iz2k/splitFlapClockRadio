import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';

@Component({
  selector: 'app-spotify-search',
  templateUrl: './spotify-search.component.html',
  styleUrls: ['./spotify-search.component.css']
})
export class SpotifySearchComponent implements OnInit {
  searchType = 'track';
  searchTerms: any;
  searchResults: any;

  constructor(private backend: BackendService) { }

  ngOnInit(): void {
  }

  search(): void {
    this.clearResults();
    if (this.searchTerms !== undefined && this.searchTerms !== '')
    {
      this.backend.spotifySearch(this.searchType, this.searchTerms).subscribe(ans => {
        console.log(ans);
        this.searchResults = JSON.parse(ans);
      });
    }
  }

  clearResults(): void {
    this.searchResults = undefined;
  }

  play(result: any): void {
    console.log('play ' + result.uri);
    this.backend.spotifyPlay(result.uri).subscribe(ans => {
      console.log(ans);
    });
  }

  addToList(result: any): void {
    console.log('add ' + result.name);
    let image = 'https://ast.m.wikipedia.org/wiki/Ficheru:No_image_available.svg';
    if (result.images !== undefined){
      if (result.images.length > 0) {
        image = result.images[0].url;
      }
    }else if (result.album !== undefined){
      if (result.album.images !== undefined){
        if (result.album.images.length > 0) {
          image = result.album.images[0].url;
        }
      }
    }
    this.backend.spotifyAddItem(result.type, result.name, result.uri, image).subscribe(ans => {
      console.log(ans);
    });

  }
}
