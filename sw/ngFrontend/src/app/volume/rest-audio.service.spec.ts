import { TestBed } from '@angular/core/testing';

import { RestAudioService } from './rest-audio.service';

describe('RestAudioService', () => {
  let service: RestAudioService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RestAudioService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
