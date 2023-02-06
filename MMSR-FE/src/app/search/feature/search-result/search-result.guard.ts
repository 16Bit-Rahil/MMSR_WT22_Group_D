import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree, createUrlTreeFromSnapshot } from '@angular/router';
import { Observable, take, map } from 'rxjs';
import { SearchService } from '../../service/search.service';

@Injectable({
  providedIn: 'root'
})
export class SearchResultGuard implements CanActivate {
  constructor(
    private router: Router,
    private searchService: SearchService){
  }
  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
      
      return this.searchService.getSearchResult().pipe(
        map( result => {
          console.log(result);
          
          if (!result.content || result.content.length === 0){
            return this.router.createUrlTree(['/home']);
          }
          const searchTermn = route.paramMap.get("searchTerm");
          if(!searchTermn || searchTermn.trim() === ""){
            return this.router.createUrlTree(['404'])
          };
          return true;
        }))
  }
  
}
