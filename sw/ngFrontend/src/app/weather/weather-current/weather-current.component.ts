import { Component, OnInit } from '@angular/core';
import {BackendService} from '../../backend.service';
import {OpenWeatherService} from '../weather-apis/open-weather-map.service';

@Component({
  selector: 'app-weather-current',
  templateUrl: './weather-current.component.html',
  styleUrls: ['./weather-current.component.css']
})
export class WeatherCurrentComponent implements OnInit {

  weatherReport: any;
  weatherIconUrl: any;

  openWeatherAPI: any;

  constructor(private backend: BackendService, public openWeather: OpenWeatherService) { }

  ngOnInit(): void {
    this.backend.getApiConfig().subscribe(jsApis => {
      console.log(jsApis);
      this.parseApis(jsApis);
      this.openWeather.setApi(this.openWeatherAPI);
    });
    this.backend.getWeather().subscribe(json => {
      this.parseWeather(json);
    });
    this.backend.ioSocket.on('weatherReport', json => this.parseWeather(json));
  }

  parseApis(json): void {
    this.openWeatherAPI = json.openWeatherApi;
  }

  parseWeather(json): void {
    if (json !== null && json !== undefined && json !== {}) {
      this.weatherReport = json;
      this.weatherIconUrl = 'http://openweathermap.org/img/wn/' + this.weatherReport.current.weather[0].icon + '@4x.png';
    }
  }
}
