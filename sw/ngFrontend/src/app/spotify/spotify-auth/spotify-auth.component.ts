import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';
import {MatDialog} from '@angular/material/dialog';
import {SpotifyAuthUpdateSpotipyComponent} from './spotify-auth-update-spotipy/spotify-auth-update-spotipy.component';
import {SpotifyAuthUpdateRaspotifyComponent} from "./spotify-auth-update-raspotify/spotify-auth-update-raspotify.component";

@Component({
  selector: 'app-spotify-auth',
  templateUrl: './spotify-auth.component.html',
  styleUrls: ['./spotify-auth.component.css']
})
export class SpotifyAuthComponent implements OnInit {

  authStatus: any;
  deviceVisible: any;

  constructor(public dialog: MatDialog, private backend: BackendService) { }

  ngOnInit(): void {
    this.checkAuthStatus();
    this.checkDevice();
  }

  checkAuthStatus(): void {
    this.backend.getSpotifyAuth().subscribe(json => {
      this.authStatus = json.status;
      console.log(json);
    });
  }

  checkDevice(): void {
    this.backend.checkSpotifyDevice().subscribe(json => {
      this.deviceVisible = json.Visible;
      console.log(json);
    });
  }

  openDialogUpdateSpotifyCli(): void {
    const dialogRef = this.dialog.open(SpotifyAuthUpdateSpotipyComponent, {});

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      if (result !== undefined){
        console.log(result);
        this.authStatus = undefined;
        this.checkAuthStatus();
      }
    });
  }

  openDialogUpdateRaspotify(): void {
    const dialogRef = this.dialog.open(SpotifyAuthUpdateRaspotifyComponent, {});

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      if (result !== undefined){
        console.log(result);
        this.deviceVisible = undefined;
        this.checkDevice();
      }
    });
  }

}
