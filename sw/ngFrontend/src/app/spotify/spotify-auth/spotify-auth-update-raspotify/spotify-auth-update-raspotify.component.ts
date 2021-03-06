import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';
import {RestSpotifyService} from '../../rest-spotify.service';

@Component({
  selector: 'app-spotify-auth-update-raspotify',
  templateUrl: './spotify-auth-update-raspotify.component.html',
  styleUrls: ['./spotify-auth-update-raspotify.component.css']
})
export class SpotifyAuthUpdateRaspotifyComponent implements OnInit {
  username: any;
  password: any;
  updateInCurse = false;

  constructor(
    public dialogRef: MatDialogRef<SpotifyAuthUpdateRaspotifyComponent>,
    private restSpotify: RestSpotifyService,
    @Inject(MAT_DIALOG_DATA) public alarm: any) { }

  ngOnInit(): void {
  }

  updateRaspotify(): void {
    console.log('Updating Raspotify credentials');
    this.updateInCurse = true;

    this.restSpotify.spotifyUpdateRaspotifyCredentials(this.username, this.password).subscribe(ans => {
      console.log(ans);
      this.updateInCurse = false;
      this.dialogRef.close('json');
    });
  }

}
