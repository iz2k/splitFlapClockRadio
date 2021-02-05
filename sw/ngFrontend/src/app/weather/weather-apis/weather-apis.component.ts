import { Component, OnInit } from '@angular/core';
import {GeocodeService} from './geocode.service';
import {OpenWeatherService} from './open-weather-map.service';
import {RestWeatherService} from '../rest-weather.service';

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

  constructor(private restWeather: RestWeatherService,
              public geocode: GeocodeService,
              public openWeather: OpenWeatherService) { }

  ngOnInit(): void {
      this.restWeather.getApis().subscribe(jsApis => {
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
    this.restWeather.setApis(
      [
        {parameter: 'geocodeApi', value: this.geocodeAPI}
      ]).subscribe(json =>
    {
        console.log(json);
        this.parseApis(json);
        this.restWeather.reloadWeather().subscribe();
    });
  }

  saveOpenWeatherApi(): void {
    this.openWeather.setApi(this.openWeatherAPI);
    this.restWeather.setApis(
      [
        {parameter: 'openWeatherApi', value: this.openWeatherAPI}
      ]).subscribe(json =>
    {
        console.log(json);
        this.parseApis(json);
        this.restWeather.reloadWeather().subscribe();
    });
  }
}
