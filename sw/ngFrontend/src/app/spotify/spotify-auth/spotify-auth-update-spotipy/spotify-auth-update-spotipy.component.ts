import {Component, Inject, OnInit} from '@angular/core';
import {BackendService} from '../../../backend.service';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

@Component({
  selector: 'app-spotify-auth-update-spotipy',
  templateUrl: './spotify-auth-update-spotipy.component.html',
  styleUrls: ['./spotify-auth-update-spotipy.component.css']
})
export class SpotifyAuthUpdateSpotipyComponent implements OnInit {

  authURL: any;
  verificationCode: any;
  constructor(
    public dialogRef: MatDialogRef<SpotifyAuthUpdateSpotipyComponent>,
    private backend: BackendService,
    @Inject(MAT_DIALOG_DATA) public alarm: any) { }

  ngOnInit(): void {
    this.startAuth();
    this.backend.ioSocket.on('spotipy-auth', json => this.parseSpotipyAuth(json));
  }

  private parseSpotipyAuth(json): void {
    console.log(json);
    if (json[0] === 'reqUrl')
    {
      this.authURL = json[1];
    }
    if (json[0] === 'setCode')
    {
      this.dialogRef.close('New credentials set');
    }
  }

  startAuth(): void {
    this.backend.ioSocket.emit('spotipy-auth', ['reqUrl', '']);
  }

  endAuth(): void {
    this.backend.ioSocket.emit('spotipy-auth', ['setCode', this.verificationCode]);
  }

}
