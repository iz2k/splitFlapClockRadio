import {Component, OnInit, ViewChild} from '@angular/core';
import {WeatherCurrentComponent} from '../weather-current/weather-current.component';
import {BackendService} from '../../backend.service';
import Map from 'ol/Map';
import TileLayer from 'ol/layer/Tile';
import OSM from 'ol/source/OSM';
import View from 'ol/View';
import * as olProj from 'ol/proj';
import {GeocodeService} from './geocode.service';

@Component({
  selector: 'app-location-config',
  templateUrl: './location-config.component.html',
  styleUrls: ['./location-config.component.css']
})
export class LocationConfigComponent implements OnInit {

  cityName = '';
  geocodeAPI: any;
  geocodeResult: any;
  volatileCityName: any;
  volatileGeocodeAPI: any;
  location: any;
  map: any;

  @ViewChild(WeatherCurrentComponent)
  private weatherCurrent: WeatherCurrentComponent;

  constructor(private backend: BackendService, private geocode: GeocodeService) { }

  ngOnInit(): void {
    this.backend.getLocationConfig().subscribe(jsLocation => {
      console.log(jsLocation);
      this.parseLocationConfig(jsLocation);
      this.backend.getApiConfig().subscribe(jsApis => {
        console.log(jsApis);
        this.parseApis(jsApis);
        this.searchCity();
      });
      this.map = new Map({
        controls: [],
        target: 'cityMap',
        layers: [
          new TileLayer({
            source: new OSM()
          })
        ],
        view: new View({
          center: olProj.fromLonLat([0, 0]),
          zoom: 1
        })
      });

    });
  }

  parseLocationConfig(json): void {
    this.cityName = json.city;
    this.volatileCityName = this.cityName;
  }

  parseApis(json): void {
    this.geocodeAPI = json.geocodeApi;
    this.volatileGeocodeAPI = this.geocodeAPI;
    this.geocode.setApi(this.geocodeAPI);
  }

  searchCity(): void {
    this.geocode.getCityGeocode(this.cityName).subscribe(json => {
      this.geocodeResult = json;
      console.log('Geocode result:');
      console.log(this.geocodeResult);
      if (this.geocodeResult.features[0] !== undefined)
      {
        this.location = this.geocodeResult.features[0];
        this.map.setView(new View({
          center: olProj.fromLonLat(this.location.geometry.coordinates),
          zoom: 13
        }));
      }else
      {
        this.location = undefined;
        this.map.setView(new View({
          center: olProj.fromLonLat([0, 0]),
          zoom: 1
        }));
      }
      console.log(this.location);
    });
  }

  saveLocation(): void {
    this.backend.setLocationParameters(
      [
        {parameter: 'city', value: this.location.properties.name},
        {parameter: 'longitude', value: this.location.geometry.coordinates[0]},
        {parameter: 'latitude', value: this.location.geometry.coordinates[1]}
      ]).subscribe(json =>
    {
      this.parseLocationConfig(json);
      this.backend.reloadWeather().subscribe();
    });
  }

  saveGeocodeApi(): void {
    this.backend.setApiParameters(
      [
        {parameter: 'geocodeApi', value: this.geocodeAPI}
      ]).subscribe(json =>
    {
      this.parseLocationConfig(json);
    });
  }

}
