import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ClockCurrentComponent } from './clock-current.component';

describe('ClockCurrentComponent', () => {
  let component: ClockCurrentComponent;
  let fixture: ComponentFixture<ClockCurrentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ClockCurrentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ClockCurrentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
