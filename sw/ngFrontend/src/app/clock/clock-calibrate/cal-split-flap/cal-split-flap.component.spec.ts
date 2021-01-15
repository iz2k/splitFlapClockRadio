import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CalSplitFlapComponent } from './cal-split-flap.component';

describe('CalSplitFlapComponent', () => {
  let component: CalSplitFlapComponent;
  let fixture: ComponentFixture<CalSplitFlapComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CalSplitFlapComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CalSplitFlapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
