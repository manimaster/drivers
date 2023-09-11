package mongodb

import (
	"context"
	"os"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type MongoDB struct {
	Client *mongo.Client
	Ctx    context.Context
}

func Connect() (*MongoDB, error) {
	uri := os.Getenv("MONGO_URI")
	client, err := mongo.NewClient(options.Client().ApplyURI(uri))
	if err != nil {
		return nil, err
	}

	ctx := context.Background()
	err = client.Connect(ctx)
	if err != nil {
		return nil, err
	}

	db := &MongoDB{Client: client, Ctx: ctx}
	return db, nil
}

func (db *MongoDB) InsertDocument(database, collection string, document interface{}) (*mongo.InsertOneResult, error) {
	col := db.Client.Database(database).Collection(collection)
	return col.InsertOne(db.Ctx, document)
}

func (db *MongoDB) FindDocument(database, collection string, filter bson.M) (*mongo.SingleResult, error) {
	col := db.Client.Database(database).Collection(collection)
	return col.FindOne(db.Ctx, filter), nil
}

func (db *MongoDB) UpdateDocument(database, collection string, filter, update bson.M) (*mongo.UpdateResult, error) {
	col := db.Client.Database(database).Collection(collection)
	return col.UpdateOne(db.Ctx, filter, update)
}

func (db *MongoDB) DeleteDocument(database, collection string, filter bson.M) (*mongo.DeleteResult, error) {
	col := db.Client.Database(database).Collection(collection)
	return col.DeleteOne(db.Ctx, filter)
}

func (db *MongoDB) Disconnect() error {
	return db.Client.Disconnect(db.Ctx)
}
