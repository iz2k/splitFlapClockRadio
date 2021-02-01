import {Component, Inject, OnInit} from '@angular/core';
import {BackendService} from '../../../backend.service';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";

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
  }

  startAuth(): void {
    this.backend.startSpotifyAuth().subscribe(json => {
      console.log(json);
      if (json.url !== null){
        this.authURL = json.url;
      }else{
        this.startAuth();
      }
    });
  }

  endAuth(): void {
    this.backend.endSpotifyAuth(this.verificationCode).subscribe(json => {
      console.log(json);
      this.dialogRef.close('json');
    });
  }
}
