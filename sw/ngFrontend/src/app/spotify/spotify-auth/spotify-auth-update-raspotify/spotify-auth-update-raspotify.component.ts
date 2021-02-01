import {Component, Inject, OnInit} from '@angular/core';
import {BackendService} from '../../../backend.service';
import {MAT_DIALOG_DATA, MatDialogRef} from '@angular/material/dialog';

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
    private backend: BackendService,
    @Inject(MAT_DIALOG_DATA) public alarm: any) { }

  ngOnInit(): void {
  }

  updateRaspotify(): void {
    console.log('Updating Raspotify credentials');
    this.updateInCurse = true;

    this.backend.spotifyUpdateRaspotifyCredentials(this.username, this.password).subscribe(ans => {
      console.log(ans);
      this.updateInCurse = false;
      this.dialogRef.close('json');
    });
  }

}
