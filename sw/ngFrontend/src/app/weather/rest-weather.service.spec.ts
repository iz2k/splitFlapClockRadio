import { TestBed } from '@angular/core/testing';

import { RestWeatherService } from './rest-weather.service';

describe('RestWeatherService', () => {
  let service: RestWeatherService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RestWeatherService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
