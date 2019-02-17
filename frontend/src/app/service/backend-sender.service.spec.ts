import { TestBed } from '@angular/core/testing';

import { BackendSenderService } from './backend-sender.service';

describe('BackendSenderService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: BackendSenderService = TestBed.get(BackendSenderService);
    expect(service).toBeTruthy();
  });
});
