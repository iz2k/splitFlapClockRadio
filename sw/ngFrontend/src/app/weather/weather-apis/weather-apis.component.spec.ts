import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WeatherApisComponent } from './weather-apis.component';

describe('WeatherApisComponent', () => {
  let component: WeatherApisComponent;
  let fixture: ComponentFixture<WeatherApisComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WeatherApisComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WeatherApisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
