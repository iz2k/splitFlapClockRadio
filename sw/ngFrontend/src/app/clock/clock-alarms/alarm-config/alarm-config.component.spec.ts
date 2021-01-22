import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlarmConfigComponent } from './alarm-config.component';

describe('AlarmConfigComponent', () => {
  let component: AlarmConfigComponent;
  let fixture: ComponentFixture<AlarmConfigComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AlarmConfigComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AlarmConfigComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
