import { TestBed } from '@angular/core/testing';

import { RestClockService } from './rest-clock.service';

describe('RestClockService', () => {
  let service: RestClockService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RestClockService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
