import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClockCalibrateComponent } from './clock-calibrate.component';

describe('ClockCalibrateComponent', () => {
  let component: ClockCalibrateComponent;
  let fixture: ComponentFixture<ClockCalibrateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ClockCalibrateComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ClockCalibrateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
