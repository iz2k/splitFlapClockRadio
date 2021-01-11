import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SensorsCurrentComponent } from './home-current.component';

describe('HomeCurrentComponent', () => {
  let component: SensorsCurrentComponent;
  let fixture: ComponentFixture<SensorsCurrentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SensorsCurrentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SensorsCurrentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
