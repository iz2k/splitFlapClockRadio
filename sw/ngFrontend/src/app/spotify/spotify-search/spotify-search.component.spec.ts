import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpotifySearchComponent } from './spotify-search.component';

describe('SpotifySearchComponent', () => {
  let component: SpotifySearchComponent;
  let fixture: ComponentFixture<SpotifySearchComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SpotifySearchComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SpotifySearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
