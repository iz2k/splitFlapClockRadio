import { TestBed } from '@angular/core/testing';

import { RestAlarmsService } from './rest-alarms.service';

describe('ClockAlarmsBackendService', () => {
  let service: RestAlarmsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RestAlarmsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
