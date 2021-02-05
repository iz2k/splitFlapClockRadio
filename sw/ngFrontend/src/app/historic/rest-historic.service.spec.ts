import { TestBed } from '@angular/core/testing';

import { RestHistoricService } from './rest-historic.service';

describe('RestHistoricService', () => {
  let service: RestHistoricService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RestHistoricService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
