import { Injectable } from '@angular/core';
import {BackendService} from '../backend.service';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RestRadioService {


  constructor(private backend: BackendService){}


  getRadioStatus(): Observable<any> {
    return this.backend.get('/rest/radio/get-status');
  }

  tuneRadio(freq): Observable<any> {
    return this.backend.get('/rest/radio/tune?freq=' + freq);
  }

  getRadioItems(): Observable<any> {
    return this.backend.get('/rest/radio/get-items');
  }

  addRadioItem(freq, name): Observable<any> {
    return this.backend.post('/rest/radio/add-item', [freq, name]);
  }

  deleteRadioItem(idx): Observable<any> {
    return this.backend.get('/rest/radio/delete-item?idx=' + idx);
  }

}
