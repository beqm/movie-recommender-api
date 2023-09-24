

from ga.algorithm import Algorithm
from sqlalchemy.orm import Session
from fastapi import Depends
import numpy as np
import math 

from db.database import get_db
from db.repositories import UserRepository, MovieRepository, RatingsRepository

class MyGeneticAlgorithm(Algorithm):

    def __init__(self, query_search, individual_size, population_size, p_crossover, p_mutation, all_ids, max_generations=100, size_hall_of_fame=1, fitness_weights=(1.0, ), seed=42, db=None) -> None:


        super().__init__(
            individual_size, 
            population_size, 
            p_crossover, 
            p_mutation, 
            all_ids, 
            max_generations, 
            size_hall_of_fame, 
            fitness_weights, 
            seed)
        
        self.db = db
        self.all_ids = all_ids
        self.query_search = query_search
        

    

    def evaluate(self, individual):
        if not self.has_duplicates(individual):
            return (0.0,)

        ratings_movies = RatingsRepository.find_by_movieid_list(self.db, individual)
        fitness = self.fitness(ratings_movies)

        return (fitness, )
    
    def has_duplicates(self, individual):
        if len(individual) != len(set(individual)):
            return False

        invalid_ids = set(individual) - set(self.all_ids)
        if invalid_ids:
            return False

        return True

    def fitness(self, ratings_movies):
        if len(ratings_movies) > 0:
            weight = self.weight(ratings_movies)
            mean_ = weight / np.mean([obj_.rating for obj_ in ratings_movies])
        else:
            mean_ = 0.0

        return mean_
    
    def weight(self, ratings_movies):
        if len(ratings_movies) > 0:
            total_rating = sum(obj_.rating for obj_ in ratings_movies)
            average_rating = total_rating / len(ratings_movies)

            if average_rating >= 4.0:
                weight = 0.5 
            else:
                weight = 0.1 
        else:
            weight = 0.0 

        return weight

