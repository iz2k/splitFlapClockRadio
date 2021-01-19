import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpotifyListComponent } from './spotify-list.component';

describe('SpotifyListComponent', () => {
  let component: SpotifyListComponent;
  let fixture: ComponentFixture<SpotifyListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SpotifyListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SpotifyListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
