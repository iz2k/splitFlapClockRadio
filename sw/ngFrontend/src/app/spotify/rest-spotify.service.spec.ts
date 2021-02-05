import { TestBed } from '@angular/core/testing';

import { RestSpotifyService } from './rest-spotify.service';

describe('RestSpotifyService', () => {
  let service: RestSpotifyService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RestSpotifyService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
