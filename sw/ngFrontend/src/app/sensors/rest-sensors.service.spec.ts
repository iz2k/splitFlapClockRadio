import { TestBed } from '@angular/core/testing';

import { RestSensorsService } from './rest-sensors.service';

describe('RestSensorsService', () => {
  let service: RestSensorsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RestSensorsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
