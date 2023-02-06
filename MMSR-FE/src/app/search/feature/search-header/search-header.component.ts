import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NbLayoutModule, NbSearchComponent, NbSearchModule, NbSearchService } from '@nebular/theme';
import { SearchService } from '../../service/search.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-header',
  standalone: true,
  imports: [
    CommonModule, 
    NbLayoutModule, 
    NbSearchModule
  ],
  templateUrl: './search-header.component.html',
  styleUrls: ['./search-header.component.css']
})
export class SearchHeaderComponent implements OnInit {

  constructor(
    private searchService: SearchService,
    private nbSearchService: NbSearchService,
    private router: Router) { 
    this.nbSearchService.onSearchSubmit().subscribe(s => {
      this.searchService.search(s.term)
    })
  }

  ngOnInit(): void {
  }

}
