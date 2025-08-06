import { Injectable } from '@nestjs/common';
import { Repository } from 'typeorm';
import { User } from '../entities/user.entity';

@Injectable()
export class UserRepository extends Repository<User> {
  findByEmail(email: string): Promise<User | null> {
    // Simulated query
    return this.findOne({ where: { email } });
  }
}
