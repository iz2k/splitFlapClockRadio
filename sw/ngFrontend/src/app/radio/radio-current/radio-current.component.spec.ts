import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RadioCurrentComponent } from './radio-current.component';

describe('RadioCurrentComponent', () => {
  let component: RadioCurrentComponent;
  let fixture: ComponentFixture<RadioCurrentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RadioCurrentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RadioCurrentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
