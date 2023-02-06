import {ChangeDetectionStrategy, Component, OnInit} from '@angular/core';
import {SearchService} from "../../service/search.service";
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-search-result',
  templateUrl: './search-result.component.html',
  styleUrls: ['./search-result.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class SearchResultComponent{

  currentPage = 0;
  searchTerm = "";
  searchResult$ = this.searchService.getSearchResult()
  constructor(private activatedRoute: ActivatedRoute,
    private searchService: SearchService) {
      this.activatedRoute.paramMap.subscribe(params => this.searchTerm = params.get("searchTerm")!);
  }

  loadMore(){
    this.currentPage++;
    this.searchService.loadMore(this.searchTerm,this.currentPage)
  }
}
