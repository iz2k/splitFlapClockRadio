import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpotifyAuthUpdateSpotipyComponent } from './spotify-auth-update-spotipy.component';

describe('SpotifyAuthUpdateSpotipyComponent', () => {
  let component: SpotifyAuthUpdateSpotipyComponent;
  let fixture: ComponentFixture<SpotifyAuthUpdateSpotipyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SpotifyAuthUpdateSpotipyComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SpotifyAuthUpdateSpotipyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
