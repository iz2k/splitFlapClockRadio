import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';
import {GeocodeService} from './geocode.service';
import {OpenWeatherService} from './open-weather-map.service';

@Component({
  selector: 'app-weather-apis',
  templateUrl: './weather-apis.component.html',
  styleUrls: ['./weather-apis.component.css']
})
export class WeatherApisComponent implements OnInit {

  geocodeAPI: any;
  storedGeocodeAPI: any;
  openWeatherAPI: any;
  storedOpenWeatherAPI: any;

  constructor(private backend: BackendService,
              public geocode: GeocodeService,
              public openWeather: OpenWeatherService) { }

  ngOnInit(): void {
      this.backend.getApiConfig().subscribe(jsApis => {
        console.log(jsApis);
        this.parseApis(jsApis);
        this.geocode.setApi(this.geocodeAPI);
        this.openWeather.setApi(this.openWeatherAPI);
      });
  }

  parseApis(json): void {
    this.geocodeAPI = json.geocodeApi;
    this.storedGeocodeAPI = this.geocodeAPI;
    this.openWeatherAPI = json.openWeatherApi;
    this.storedOpenWeatherAPI = this.openWeatherAPI;
  }

  saveGeocodeApi(): void {
    this.geocode.setApi(this.geocodeAPI);
    this.backend.setApiParameters(
      [
        {parameter: 'geocodeApi', value: this.geocodeAPI}
      ]).subscribe(json =>
    {
        console.log(json);
        this.parseApis(json);
        this.backend.reloadWeather().subscribe();
    });
  }

  saveOpenWeatherApi(): void {
    this.openWeather.setApi(this.openWeatherAPI);
    this.backend.setApiParameters(
      [
        {parameter: 'openWeatherApi', value: this.openWeatherAPI}
      ]).subscribe(json =>
    {
        console.log(json);
        this.parseApis(json);
        this.backend.reloadWeather().subscribe();
    });
  }
}
