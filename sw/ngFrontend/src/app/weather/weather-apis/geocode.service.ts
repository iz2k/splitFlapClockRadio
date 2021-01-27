import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class GeocodeService {

  private urlEndPoint = 'https://app.geocodeapi.io/api/v1';
  private apiKey: any;
  isOk = false;
  checkInCurse = false;

  constructor(private http: HttpClient) {
    console.log('Creating Geocode Service');
  }

  setApi(key): void {
    this.apiKey = key;
    this.checkApi();
  }

  getCityGeocode(city): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/search?text=' + city + '&apikey=' + this.apiKey);
  }

  checkApi(): void {
    this.isOk = false;
    this.checkInCurse = true;
    this.getCityGeocode('Donostia').subscribe(json => {
      this.checkInCurse = false;
      if (json.features[0] !== undefined) {
        this.isOk = true;
      }
    }, error => {
      this.checkInCurse = false;
    });
  }

}
