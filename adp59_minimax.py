import itertools
import copy

##########################
###### MINI-MAX A-B ######
##########################

class AlphaBeta:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game_tree):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.root  # GameNode
        return

    # Do an AB Search with cutoff at depth and time
    def alpha_beta_search(self, node):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity

        successors = self.getSuccessors(node)
        best_state = None
        for state in successors:
            value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        #print "AlphaBeta:  Utility Value of Root Node: = " + str(best_val)
        if best_state is not None:
            print "AlphaBeta:  Best State is: " + best_state.name
        return best_state

    def max_value(self, node, alpha, beta):
        #print "AlphaBeta-->MAX: Visited Node :: " + node.name
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = -infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        #print "AlphaBeta-->MIN: Visited Node :: " + node.name
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value
    #                     #
    #   UTILITY METHODS   #
    #                     #
    # ---> these need to be supported by the game class itself, going forward.

    # successor states in a game tree are the child nodes...
    def getSuccessors(self, node):
        assert node is not None
        return node.children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def getUtility(self, node):
        assert node is not None
        return node.value


#########################
###### GAME OBJECT ######
#########################
class GameNode:
    """ Node within the game tree
    """
    def __init__(self, board, name, playerWhite):
        self.name  = name  # String, the full move including the arrow move
        self.board = copy.deepcopy(board)  # a copy of the board object, at this current state
        self.children = []
        # self.board_state = copy.deepcopy(board.config)
        self.white_turn = board.bWhite
        self.playerWhite = playerWhite

        # if we are at the root node, don't go any further
        # base case, for root node
        if name is None:
            return

        # recursive case, for other nodes
        # update board to include new move
        #self.updateBoardWithMove()

        # compute positional value of new board location
        self.black_moves = 0
        self.white_moves = 0
        (self.value, self.white_moves, self.black_moves) = self.getValue()
        #(self.white_moves, self.black_moves) = self.getValue()  # int, value of the position from this node's perspective
        return

    def addChildNode(self, node):
        self.children.append(node)

    def getValue(self):
        value = 0

        # GOAL: of the game is to MINIMIZE opponent's moves
        #       So, for now, always store white moves.
        #       That way, I want to maximize this, and opponent wants to minimize it...
        (white_moves, black_moves) = self.updateBoardWithMove()

        ###########################
        #### DEFENSIVE PLAYER #####
        ###########################
        # Maximize YOUR free spaces
        # Store values w/r/t which player we are
        if self.playerWhite:
            value = white_moves
        else:
            value = black_moves

        ###########################
        #### OFFENSIVE PLAYER #####
        ###########################
        """
        >>> Uncomment to play offensively
        # Minimize OPPONENT'S free spaces
        # Store values w/r/t which player we are
        if self.playerWhite:
            value = -black_moves
        else:
            value = -white_moves
        """

        return (value, white_moves, black_moves)


    def updateBoardWithMove(self):
        """
        The is node represents a new board state
        The node's name has the moves we need
        :return:
        """
        # get the move as a string
        move_str = self.getMove()
        # map from str --> rc format
        (src, dst) = map(self.ld2rc, move_str.split('-'))
        # move the queen in our internal board object
        self.board.move_queen(src, dst)

        # get the arrow as a string
        arrow_str = self.getArrow()
        # map from str --> rc format
        arr_dst = self.ld2rc(arrow_str)
        # shoot the arrow in our internal board object
        self.board.shoot_arrow(arr_dst)

        # end the turn in our internal object
        (w, b) = self.board.end_turn()
        #(w,b) = self.board.count_areas()

        return (w,b)


    def getSrc(self):
        # return None if we are at root
        if self.name is None:
            return None
        # otherwise, return first 2 char
        return self.name[0:2]

    def getDst(self):
        # return None if we are at root
        if self.name is None:
            return None
        # otherwise, return chars 3 -> 4
        return self.name[3:5]

    def getMove(self):
        # return None if we are at root
        if self.name is None:
            return None
        # otherwise, return chars 0 -> 5
        return self.name[0:5]

    def getArrow(self):
        # return None if we are at root
        if self.name is None:
            return None
        # otherwise, return chars 6 -> end
        return self.name[6:8]

# utility functions:
# ld2rc -- takes a string of the form, letter-digit (e.g., "a3")
# and returns a tuple in (row, column): (3,0)
# rc2ld -- takes a tuple of the form (row, column) -- e.g., (3,0)
# and returns a string of the form, letter-digit (e.g., "a3")
    def ld2rc(self, raw_loc):
        return (int(raw_loc[1]), ord(raw_loc[0])-ord('a'))

    def rc2ld(self, tup_loc):
        return chr(tup_loc[1]+ord('a'))+str(tup_loc[0])





class GameTree:
    """ The Game tree from current position
    """
    def __init__(self, queen_moves, board, playerWhite):
        self.playerWhite = playerWhite
        self.root = GameNode(board, None, self.playerWhite)
        self.board = board
        self.move_list = queen_moves

        # populate the tree -- ply 1
        self.addAllMovesNextPly(queen_moves, self.root)

        # populate ply2
        # get all queen moves again
        for node in self.root.children:
            future_board = copy.deepcopy(node.board)
            """
            # interior calls rely on self.board... need to fix that.
            # but checking for now if this works
            """
            self.board = future_board
            game = Game(future_board)
            # getAllMoves
            queenLocations = game.getQueenLocations()
            allMoves = game.getAllFutureQueenLocations(queenLocations)
            next_queen_moves = game.getAllMovesForQueens(allMoves)
            # add all the queens to all those nodes
            self.addAllMovesNextPly(next_queen_moves, node)
        """
        # revert back to correct board for the root...
        """
        self.board = board
        return

    # [Queen Moves] --> [Nodes]
    def addAllMovesNextPly(self, queen_moves, root_node):
        for move_list in queen_moves:
            node_list = self.queenMovesToNodes(move_list)

            # add each child node to the root's list, this gives us ply 1
            for node in node_list:
                root_node.addChildNode(node)
        return


    # [ All moves per queen] --> [ Nodes ]
    def queenMovesToNodes(self, move_list_per_queen):
        node_list = []
        # transform queen state indices to a string
        queen_state_raw = move_list_per_queen[0]
        queen_src = self.yx2boardInds(queen_state_raw)

        # iterate through the moves list
        for elem in move_list_per_queen[1]:
            for move in elem:
                # transform queen dst
                queen_dst_raw = move[0]
                queen_dst = self.yx2boardInds(queen_dst_raw)

                # transform arrow dst
                arrow_dst_raw = move[1]
                arrow_dst = self.yx2boardInds(arrow_dst_raw)

                # create the node
                move_str = self.contstructMoveString(queen_src, queen_dst, arrow_dst)
                node = GameNode(self.board, move_str, self.playerWhite)

                # add that node to the node list
                node_list.append(node)
        return node_list

    # transform indices to string that the game can take as input
    def yx2boardInds(self, ind_tuple):
        # get the values
        col = ind_tuple[1]
        row = ind_tuple[0]

        # transform to ascii
        col_ascii = 97 + col  # transform num --> lowercase ascii
        col_ascii = chr(col_ascii)

        # store as a string
        location_str = ""
        location_str = location_str + col_ascii + str(row)

        # return that string
        return location_str

    def contstructMoveString(self, src, dst, arr):
        seq = (src, dst, arr)
        return "-".join(seq)



class Game:
    """
    Object to encapsulate the WHOLE game we are playing
    """
    def __init__(self, board):
        self.initial_state = None
        self.current_state = None
        self.game_tree = None
        self.game_board = board.config
        self.board = board


    def player(self, node):
        # given a state, determine current player
        # accept a node --> return what player is up
        if node.bWhite:
            return 'w'
        else:
            return 'b'

    #                 #
    #     HELPERS     #
    #                 #
    def setGameTree(self, tree):
        self.game_tree = tree

    def getQueenLocations(self):
        # get locations of all the queens
        # return  a list with locations in tuples, (y,x)
        # need to know whether you are Q or q though.... how?
        if self.board.bWhite:
            matchChar = 'Q'
        else:
            matchChar = 'q'

        queenList = []
        # get uppercase queens
        for row in xrange(0, len(self.game_board)):
            for col in xrange(0, len(self.game_board)):
                if self.game_board[row][col] == matchChar:
                    queenList.append((row, col))
        return queenList


    def getValidDiags(self, location):
        #--> iterate until no longer in bounds or hit an x, or a queen.. anything but a '.'
        # create our list
        diagonalsList = []

        # store the board size, to make code simpler
        boardSize = len(self.game_board)-1 # subtracting one because we are checking indices

        # ground the location so we know where we're starting from
        row = location[0]
        col = location[1]

        #--------------------------
        #   Bottom Left Diagonal
        #--------------------------
        # -1 row, -1 col
        r = row
        c = col
        valid = True
        while valid:
            # update the row/col values
            r -= 1
            c -= 1

            # protect against out of bounds
            if r < 0 or c < 0:
                break

            # pull out the value
            v = self.game_board[r][c]
            if not v == '.':
                break
            # otherwise, we have a '.', and the cell is valid
            else:
                diagonalsList.append((r, c))

        #--------------------------
        #    Top Right Diagonal
        #--------------------------
        # +1 row, +1 col
        r = row
        c = col
        valid = True
        while valid:
            # update the row/col values
            r += 1
            c += 1

            # protect against out of bounds
            if r > boardSize or c > boardSize:
                break

            # pull out the value
            v = self.game_board[r][c]
            if not v == '.':
                break
            # otherwise, we have a '.', and the cell is valid
            else:
                diagonalsList.append((r, c))

        #--------------------------
        #   Bottom Right Diagonal
        #--------------------------
        # -1 row, +1 col
        r = row
        c = col
        valid = True
        while valid:
            # update the row/col values
            r -= 1
            c += 1
            # protect against out of bounds
            if r < 0 or c > boardSize:
                break

            # pull out the value
            v = self.game_board[r][c]
            if not v == '.':
                break
            # otherwise, we have a '.', and the cell is valid
            else:
                diagonalsList.append((r, c))

        #--------------------------
        #    Top Left Diagonal
        #--------------------------
        # +1 row, -1 col
        r = row
        c = col
        valid = True
        while valid:
            # update the row/col values
            r += 1
            c -= 1
            # protect against out of bounds
            if r > boardSize or c < 0:
                break

            # pull out the value
            v = self.game_board[r][c]
            if not v == '.':
                break
            # otherwise, we have a '.', and the cell is valid
            else:
                diagonalsList.append((r, c))

        # return the list, now that we're all done
        return diagonalsList


    def getValidVerts(self, location):
        #--> iterate until no longer in bounds or hit an x, or a queen.. anything but a '.'
        # create our list
        vertsList = []

        # store the board size, to make code simpler
        boardSize = len(self.game_board)-1 # subtracting one because we are checking indices

        # ground the location so we know where we're starting from
        row = location[0]
        col = location[1]

        #--------------------------
        #         Top Rows
        #--------------------------
        # row+1, col=same
        r = row
        c = col
        valid = True
        while valid:
            # update the row/col values
            r += 1

            # protect against out of bounds
            if r > boardSize:
                break

            # pull out the value
            v = self.game_board[r][c]
            if not v == '.':
                break
            # otherwise, we have a '.', and the cell is valid
            else:
                vertsList.append((r, c))

        #--------------------------
        #        Bottom Rows
        #--------------------------
        # row-1, col=same
        r = row
        c = col
        valid = True
        while valid:
            # update the row/col values
            r -= 1

            # protect against out of bounds
            if r < 0:
                break

            # pull out the value
            v = self.game_board[r][c]
            if not v == '.':
                break
            # otherwise, we have a '.', and the cell is valid
            else:
                vertsList.append((r, c))

        # return the verticals we've found
        return vertsList


    def getValidHorz(self, location):
        #--> iterate until no longer in bounds or hit an x, or a queen.. anything but a '.'
        # create our list
        horzList = []

        # store the board size, to make code simpler
        boardSize = len(self.game_board)-1 # subtracting one because we are checking indices

        # ground the location so we know where we're starting from
        row = location[0]
        col = location[1]

        #--------------------------
        #       Right Cols
        #--------------------------
        # row=same, col+1
        r = row
        c = col
        valid = True
        while valid:
            # update the row/col values
            c += 1

            # protect against out of bounds
            if c > boardSize:
                break

            # pull out the value
            v = self.game_board[r][c]
            if not v == '.':
                break
            # otherwise, we have a '.', and the cell is valid
            else:
                horzList.append((r, c))

        #--------------------------
        #        Left Cols
        #--------------------------
        # row=same, col-1
        r = row
        c = col
        valid = True
        while valid:
            # update the row/col values
            c -= 1

            # protect against out of bounds
            if c < 0:
                break

            # pull out the value
            v = self.game_board[r][c]
            if not v == '.':
                break
            # otherwise, we have a '.', and the cell is valid
            else:
                horzList.append((r, c))

        # return the verticals we've found
        return horzList

    # Location (x,y) -> [ Locations ]
    def getValidMoves(self, location_tuple):
        """
        General method to get all valid 'moves' from some (y,x) coord
        :param location_tuple: (y,x)
        :return: a list of location tuples
        """
        # given queen location-->OR<--an arrow location, find all valid moves
        # for all the elements...
        diags = self.getValidDiags(location_tuple)
        verts = self.getValidVerts(location_tuple)
        horz = self.getValidHorz(location_tuple)

        # concat them all
        validMoves = diags + verts + horz

        # build all queen moves from current step
        # pass in all queen moves and concat on the possible arrow moves to each
        # that list is the return value
        return validMoves

    # [Queen Locations (y,x)] -> [(Location, [All Locations])
    def getAllFutureQueenLocations(self, queenLocations):
        """
        Take the list of current queen locations, and output a list that contains
        [ (Queen Location Now, [ All Possible Future Locations in next Move) ]
        @param list of queen locations
        :return:  List with the queen location and all possible future locations
        """
        # (x,y) -> ( (x,y), [(x,y) .... ])
        future_locations = []

        # get all valid moves for each queen
        for elem in queenLocations:
            # grab the moves
            validMoves = self.getValidMoves(elem)
            # then make a tuple containing (cur_location, [future locations])
            move_tuple = (elem, validMoves)
            # and add that tuple to our list
            future_locations.append(move_tuple)


        # THINK: later we can map the first location of over the future locations
        #        then same thing with arrow locations but
        return future_locations

    # [Queen Location, [All Locations]] -> [Queen Location, [(All Locations, Arrow Show)])
    def getArrowLocations(self, queen_and_its_moves):
        """
        :param queen_and_its_moves: Take a tuple of form:
                ((y,x), [dst])
        :return: [(dst), (arrow_location) ... ]
                  Everything in form (y,x) coords
        """
        # get all the destinations in future locations
        dst_and_arrow_list = []
        #for elem in queen_and_its_moves:
        dest_list = queen_and_its_moves[1]
        # take each destination, and find all possible arrow locations
        for dst in dest_list:
            arrow_shots_list = self.getValidMoves(dst)
            endpoints = itertools.repeat(dst, len(arrow_shots_list))
            dst_and_arrow_tuple = zip(endpoints, arrow_shots_list)
            dst_and_arrow_list.append(dst_and_arrow_tuple)

        #for elem in dst_and_arrow_list:
        #    print "DST AND ARROW == " + str(elem)

        # now, for each dst, all the arrow locations
        # for elem
        # index into elem[1], the tuple list of future moves,
        # and find all future moves from THAT move
        return dst_and_arrow_list

    # --> this is like concatting arrow locations with the dest locations
    # Queen Location (y,x) -> [(src_loc, dst_loc, arrow_loc)]
    def getAllMovesForQueens(self, future_locations):
        queens_and_moves = []
        for elem in future_locations:
            dst_and_arrows = self.getArrowLocations(elem)
            queens_and_moves.append((elem[0], dst_and_arrows))

        # (y,x) -> [ Locations ] ... pull out each location
        # and for get all arrow locations for each
        # make a new tuple from the arrow locations.... and concat all those as well
        return queens_and_moves
