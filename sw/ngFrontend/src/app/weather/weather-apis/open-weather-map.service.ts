import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class OpenWeatherService {

  private urlEndPoint = 'https://api.openweathermap.org/data/2.5';
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

  getWeather(lat, lon): Observable<any> {
    return this.http.get<any>(this.urlEndPoint + '/onecall?lat=' +
      lat + '&lon=' + lon +
      '&exclude=minutely&units=metric&lang=es&appid=' + this.apiKey);
  }

  checkApi(): void {
    this.isOk = false;
    this.checkInCurse = true;
    this.getWeather(0, 0).subscribe(json => {
      this.checkInCurse = false;
      if (json.current !== undefined) {
        this.isOk = true;
      }
    }, error => {
      this.checkInCurse = false;
    });
  }
}
