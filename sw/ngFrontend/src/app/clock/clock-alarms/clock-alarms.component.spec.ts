import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClockAlarmsComponent } from './clock-alarms.component';

describe('ClockAlarmsComponent', () => {
  let component: ClockAlarmsComponent;
  let fixture: ComponentFixture<ClockAlarmsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ClockAlarmsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ClockAlarmsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
