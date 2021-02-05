import { TestBed } from '@angular/core/testing';

import { RestRadioService } from './rest-radio.service';

describe('RestRadioService', () => {
  let service: RestRadioService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RestRadioService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
