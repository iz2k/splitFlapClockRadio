import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpotifyCurrentComponent } from './spotify-current.component';

describe('SpotifyCurrentComponent', () => {
  let component: SpotifyCurrentComponent;
  let fixture: ComponentFixture<SpotifyCurrentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SpotifyCurrentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SpotifyCurrentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
