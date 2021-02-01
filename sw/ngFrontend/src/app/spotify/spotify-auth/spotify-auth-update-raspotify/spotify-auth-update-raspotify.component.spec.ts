import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpotifyAuthUpdateRaspotifyComponent } from './spotify-auth-update-raspotify.component';

describe('SpotifyAuthUpdateRaspotifyComponent', () => {
  let component: SpotifyAuthUpdateRaspotifyComponent;
  let fixture: ComponentFixture<SpotifyAuthUpdateRaspotifyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SpotifyAuthUpdateRaspotifyComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SpotifyAuthUpdateRaspotifyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
